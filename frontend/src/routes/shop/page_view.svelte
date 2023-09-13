<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name = '';
	let sort = 'latest';

	let sorts = [
		'latest',
		'oldest',
		'name (a-z)',
		'name (z-a)',
		'cheap',
		'expensive',
		'discount'
		// 'rating'
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

	const submit = () => {
		set_state(page_name, 'sort', sort == 'latest' ? '' : sort);
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('sort')) {
			sort = params.get('sort');
		}
	});
</script>

<section class="line wrap">
	<Button class="small" on:click={save_view}>
		<SVG type={$user.setting.item_view == 'grid' ? 'shop_active' : 'list'} />
		view
	</Button>

	<span class="line">
		sort:
		<select bind:value={sort} on:change={submit}>
			{#each sorts as value}
				<option {value}>
					{value}
				</option>
			{/each}
		</select>
	</span>
</section>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp0);
	}
	.wrap {
		flex-wrap: wrap;
		gap: var(--sp2);
	}

	select {
		display: inline;
		padding: var(--sp0);
	}
</style>
