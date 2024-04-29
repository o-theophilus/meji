<script>
	import { onMount } from 'svelte';

	import Center from '$lib/center.svelte';
	import Item from '$lib/item/index.svelte';
	import ItemPack from '$lib/item_pack.svelte';

	export let name = 'Group Name';
	export let url = '';
	export let items = [];
	export let style = 'grid';

	onMount(async () => {
		if (url) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}${url}`);
			resp = await resp.json();

			if (resp.status == 200) {
				items = resp.items;
			}
		}
	});

	export let open = true;
	const set_open = () => {
		open = !open;
	};

	let width;
</script>

<svelte:window bind:innerWidth={width} />

{#if items && items.length > 0}
	<div id={name.toLowerCase().replace(/ /g, '_')} />

	<Center>
		<section class="card">
			<br />
			<br />
			<div class="ctitle">
				{name}
				<slot {open} {set_open} />
			</div>
			<br />

			<ItemPack let:style {style} {open}>
				{#each items.slice(0, width < 1000 ? 6 : 8) as x (x.key)}
					<Item item={x} {style} />
				{/each}
			</ItemPack>
		</section>
	</Center>
{/if}

<style>
	.card {
		border-bottom: 2px solid var(--ac4);
	}
</style>
