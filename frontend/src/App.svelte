<script>
    import { onMount } from 'svelte';

    let airports = [];
    let selectedAirport = '';
    let selectedDay = '1';
    let daysOfWeek = [
        { id: 1, name: 'Monday' },
        { id: 2, name: 'Tuesday' },
        { id: 3, name: 'Wednesday' },
        { id: 4, name: 'Thursday' },
        { id: 5, name: 'Friday' },
        { id: 6, name: 'Saturday' },
        { id: 7, name: 'Sunday' }
    ];

    let result = null;
    let loading = false;
    let error = '';

    onMount(async () => {
        const res = await fetch('http://localhost:5000/airports');
        airports = await res.json();
        if (airports.length > 0) {
            selectedAirport = airports[0].AirportID;
        }
    });

    async function predictDelay() {
        loading = true;
        error = '';
        result = null;
        try {
            const res = await fetch(
                `http://localhost:5000/predict?day_of_week=${selectedDay}&origin_airport_id=${selectedAirport}`
            );
            if (!res.ok) {
                throw new Error('Prediction failed');
            }
            result = await res.json();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }
</script>

<main>
    <h1>Flight Delay Predictor</h1>

    <label>
        Day of the week:
        <select bind:value={selectedDay}>
            {#each daysOfWeek as day}
                <option value={day.id}>{day.name}</option>
            {/each}
        </select>
    </label>

    <label>
        Airport:
        <select bind:value={selectedAirport}>
            {#each airports as airport}
                <option value={airport.AirportID}>{airport.AirportName}</option>
            {/each}
        </select>
    </label>

    <button disabled={!selectedAirport || loading} on:click={predictDelay}>
        {loading ? 'Predicting...' : 'Predict Delay Chance'}
    </button>

    {#if error}
        <p style="color: red">{error}</p>
    {/if}

    {#if result}
        <p>
            <strong>Chance of delay:</strong> {result.confidence_percent}%
        </p>
    {/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>