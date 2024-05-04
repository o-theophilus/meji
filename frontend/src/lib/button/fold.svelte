<script>
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	export let open;
</script>

<div class="fold" class:open>
	<BRound on:click>
		<SVG type="angle" size="8" />
	</BRound>
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
