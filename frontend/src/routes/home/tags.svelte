<script>
	import { onMount } from 'svelte';
	import { module, state } from '$lib/store.js';

	import Center from '$lib/card.svelte';
	import Link from '$lib/button/link.svelte';

	import Tag from './tags.btn.svelte';
	import All from './tags._all.svelte';
	import ItemPack from '$lib/item_pack.svelte';

	let width;
	let tags = [];

	onMount(async () => {
		let i = $state.findIndex((x) => x.name == 'tags');
		if (i != -1) {
			tags = $state[i].data;
		}
	});
</script>

<svelte:window bind:innerWidth={width} />

{#if tags.length > 0}
	<div id="tag" />
	<Center>
		<div class="ctitle">Tags</div>

		<Link
			on:click={() => {
				$module = {
					module: All
				};
			}}
			icon
		>
			view more
		</Link>

		<br />

		<ItemPack style="grid">
			{#each tags.slice(0, width < 1000 ? 6 : 8) as tag}
				<Tag {tag} />
			{/each}
		</ItemPack>
	</Center>
{/if}

<style>
</style>
