<script>
	export let value = '';
	export let id = '';
	export let type = '';
	export let placeholder = '';
	export let min = '';
</script>

{#if type == 'text'}
	<input bind:value {id} type="text" {placeholder} />
{:else if type == 'email'}
	<input bind:value {id} type="email" {placeholder} />
{:else if type == 'password'}
	<input bind:value {id} type="password" {placeholder} />
{:else if type == 'number'}
	<input bind:value {id} type="number" {placeholder} />
{:else if type == 'tel'}
	<input bind:value {id} type="tel" {placeholder} />
{:else if type == 'date'}
	<input bind:value {id} type="date" {placeholder} {min} />
{:else if type == 'time'}
	<input bind:value {id} type="time" {placeholder} {min} />
{:else if type == 'datetime'}
	<input bind:value {id} type="datetime-local" {placeholder} {min} />
{:else if type == 'textarea'}
	<textarea bind:value {id} {placeholder} on:blur />
{/if}

<style>
	input,
	textarea {
		width: 100%;

		padding: var(--sp1);
		border-radius: var(--sp0);
		border: none;

		outline: 2px solid var(--ac4);
		background-color: var(--ac5);
		color: var(--ac1);
	}

	input:hover,
	textarea:hover {
		outline-color: var(--ac3);
	}

	input:focus,
	textarea:focus {
		outline-color: var(--ac1);
	}

	textarea {
		display: block;
		resize: none;
		height: 160px;
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
	::-webkit-calendar-picker-indicator {
    filter: invert(0.5);
}
</style>
