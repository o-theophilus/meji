<script>
	export let value = '';
	export let id = '';
	export let type = '';
	export let placeholder = '';
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
{:else if type == 'textarea'}
	<textarea bind:value {id} {placeholder} />
{/if}

<style>
</style>
