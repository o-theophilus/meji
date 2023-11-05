<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { user } from '$lib/store.js';

	import Center from '$lib/center.svelte';
	import Item from '$lib/item/index.svelte';

	export let name = 'Group Name';
	export let url = '';
	export let items = [];

	onMount(async () => {
		if (url) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}${url}`);
			resp = await resp.json();

			if (resp.status == 200) {
				items = resp.items;
			}
		}
	});

	let open = true;
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

			{#if open}
				<div
					class="item_area"
					class:list={$user.setting.item_view == 'list'}
					transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
				>
					{#each items.slice(0, width < 1000 ? 6 : 8) as x (x.key)}
						<Item item={x} />
					{/each}
				</div>

				<br />
			{/if}
		</section>
	</Center>
{/if}

<style>
	.card {
		border-bottom: 2px solid var(--ac4);
	}

	@media screen and (min-width: 700px) {
	}
</style>
