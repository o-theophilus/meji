<script>
	import Button from '$lib/button.svelte';
	export let active = false;
	export let disabled;
</script>

<Button class="small" on:click {disabled}>
	<input type="checkbox" checked={active} {disabled} />
	<slot />
</Button>

<style>
	input {
		cursor: pointer;
	}
</style>
