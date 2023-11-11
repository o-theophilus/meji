<script>
	import Button from '$lib/button.svelte';
	export let active = false;
</script>

<Button class="small" on:click>
	<div class="check" class:active>
		<div class="mark" />
	</div>
	<slot />
</Button>

<style>
	.check {
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 2px;
		outline: 2px solid var(--ac6);

		background-color: var(--ac6);
	}
	.active {
		background-color: var(--cl1);
	}
</style>
