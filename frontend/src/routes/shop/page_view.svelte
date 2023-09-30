<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name = '';
	let sort = 'latest';
	let width;
	let open_sort = false;

	let sorts = [
		'latest',
		'oldest',
		'name (a-z)',
		'name (z-a)',
		'cheap',
		'expensive',
		'discount',
		'rating'
	];

	const save_view = async () => {
		$user.setting.item_view = $user.setting.item_view == 'grid' ? 'list' : 'grid';
		const resp = await fetch(`${import.meta.env.VITE_BACKEND}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ item_view: $user.setting.item_view })
		});
	};

	const sort_items = (x) => {
		sort = x;
		open_sort = false;
		set_state(page_name, 'sort', x == 'latest' ? '' : x);
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('sort')) {
			sort = params.get('sort');
		}
	});
</script>

<svelte:window
	on:click={() => {
		if (open_sort) {
			open_sort = false;
		}
	}}
/>

<section class="line wrap">
	<Button class="small" on:click={save_view}>
		<SVG type={$user.setting.item_view == 'grid' ? 'shop_active' : 'list'} />
		view
	</Button>

	<div bind:clientWidth={width} class="pos" on:click|stopPropagation role="presentation">
		<Button
			class="small"
			on:click={() => {
				open_sort = !open_sort;
			}}
		>
			<SVG type={$user.setting.item_view == 'grid' ? 'shop_active' : 'list'} />
			sort: {sort}
		</Button>

		{#if open_sort}
			<div class="sort" style:width="{width}px">
				{#each sorts as x}
					<button
						on:click={() => {
							sort_items(x);
						}}
					>
						{x}

						{#if x == sort}
							<span> ✓ </span>
						{/if}
					</button>
				{/each}
			</div>
		{/if}
	</div>
</section>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp0);

		color: var(--ac2);
		font-size: small;
	}
	.wrap {
		flex-wrap: wrap;
		gap: var(--sp2);
	}

	.pos {
		position: inherit;
		z-index: 1;
	}

	.sort {
		display: flex;
		flex-direction: column;

		position: absolute;

		background-color: var(--ac5);
		border-radius: var(--sp0);
		border: 2px solid var(--ac3);
	}
	button {
		display: flex;
		justify-content: space-between;

		padding: var(--sp0) var(--sp1);
		border: none;
		background: none;
		color: var(--ac2);
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ac5_);
	}
</style>
