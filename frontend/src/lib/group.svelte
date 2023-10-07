<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';

	export let name = 'Group Name';
	export let url = '';
	let items = [];

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}${url}`);
		resp = await resp.json();

		if (resp.status == 200) {
			items = resp.items;
		}
	});

	let open = true;
	const set_open = () => {
		open = !open;
	};
</script>

{#if items && items.length > 0}
	<div id={name.toLowerCase().replace(/ /g, '_')} />
	<Card>
		<div class="ctitle">
			{name}
			<slot {open} {set_open} />
		</div>

		{#if open}
			<br />
			<br />
			<div
				class="item_area"
				class:list={$user.setting.item_view == 'list'}
				transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
			>
				{#each items as x (x.key)}
					<Item item={x} />
				{/each}
			</div>
		{/if}
	</Card>
{/if}

<style>
</style>
