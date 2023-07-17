<script>
	import Button from '$lib/button.svelte';

	export let open;
</script>

<div class="fold" class:open>
	<Button icon="angle" icon_size="12" on:click />
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
