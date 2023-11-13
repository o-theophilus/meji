<script>
	import Button from '$lib/button.svelte';
	export let active = false;
</script>

<!-- <Button class="{active ? 'primary' : ''} small" on:click> -->
<Button class="small" on:click>
	<input type="checkbox" checked={active} />
	<slot />
</Button>

<style>
	input {
		cursor: pointer;
	}
</style>
