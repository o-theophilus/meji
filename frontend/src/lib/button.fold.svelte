<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let open;
</script>

<div class="fold" class:open>
	<Button class="round" on:click>
		<SVG type="angle" size="8" />
	</Button>
</div>

<style>
	.fold {
		transition: var(--trans1);
		transform: rotate(180deg);
	}
	.open {
		transform: rotate(270deg);
	}
</style>
