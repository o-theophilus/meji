<script>
	import Base from './base.svelte';

	export let adverts = [];
	export let size = '';
	let width = 0;
	let auto = '';

	$: if (width < 600) {
		auto = '300x300';
	} else if (width > 900) {
		auto = '900x300';
	} else {
		auto = '600x300';
	}
</script>

<svelte:window bind:innerWidth={width} />

{#if ['300x300', '300x600', '600x300', '900x300'].includes(size)}
	<Base {adverts} {size} />
{:else}
	<Base {adverts} size={auto} />
{/if}

<style>
</style>
