<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { user } from '$lib/store.js';

	import Center from '$lib/center.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let name = 'Group Name';
	export let url = '';
	export let shop_href = '';
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
			<div class="ctitle">
				{name}
				<slot {open} {set_open} />
			</div>

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

				{#if shop_href}
					<Button class="wide" href={shop_href}>
						view all
						<span class="rotate">
							<SVG type="angle" size="10" />
						</span>
					</Button>
				{:else}
					<br />
				{/if}
			{/if}
		</section>
	</Center>
{/if}

<style>
	.card {
		width: 100%;
		margin-top: var(--sp2);
		border-radius: var(--sp0);

		color: var(--ac2);
		background-color: var(--ac6);
		box-shadow: var(--shad1);
	}
	.ctitle {
		padding: var(--sp3);
	}
	.item_area {
		padding: 0 var(--sp3);
	}

	@media screen and (min-width: 700px) {
		.ctitle {
			padding: var(--sp5);
		}
		.item_area {
			padding: 0 var(--sp5);
		}
	}

	.rotate {
		transform: rotate(180deg);
	}
</style>
