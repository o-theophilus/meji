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
{:else if type == 'textarea'}
	<textarea bind:value {id} {placeholder} on:blur />
{/if}

<style>
</style>
