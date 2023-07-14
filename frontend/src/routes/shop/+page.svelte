<script>
	import { token } from '$lib/cookie.js';
	import { user, module, loading } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';

	import Status_Bar from './status.svelte';
	import Tag_Bar from './tag.svelte';
	import Search from './search.svelte';
	import View from './page_view.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	let { tags } = data;
	let { items } = data;
	let { total_page } = data;

	let open = true;

	const submit = async () => {
		$loading = true;
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}shop${get_query('shop')}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			$loading = false;

			if (resp.status == 200) {
				window.scrollTo({ top: 0, behavior: 'smooth' });
				items = resp.data.items;
				total_page = resp.data.total_page;
			} else {
				error = resp.message;
			}
		}
	};

	let pagination;
</script>

<Meta title="Shop" description="Shop" />

<Tag_Bar {tags} />
<Search
	on:ok={() => {
		pagination.init();
		submit();
	}}
/>
<Status_Bar />

<Pagination {total_page} />

<Card>
	<div class="title">
		Shop

		<View
			show_view={open}
			on:ok={() => {
				open = false;
				submit();
			}}
		/>
	</div>

	<div class="items" class:grid={true}>
		{#each items as item (item.key)}
			<Item {item} view_list={$user.setting.item_view == 'list'} />
		{:else}
			no item here
		{/each}
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.items {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: 1fr;

		margin-top: var(--sp4);
		color: var(--ac1);
	}
	.grid {
		grid-template-columns: repeat(2, 1fr);
	}
	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
