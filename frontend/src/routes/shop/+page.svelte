<script>
	import { token } from '$lib/cookie.js';
	import { user, module, loading } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Meta from '$lib/comp/meta.svelte';
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/item/item.svelte';

	import Search from '$lib/comp/search.svelte';
	import View from '$lib/comp/page_view.svelte';
	import Pagination from '$lib/comp/pagination.svelte';
	import Status from '$lib/comp/status_bar.svelte';
	import Button from '$lib/comp/button.svelte';
	import Button_Fold from '$lib/comp/button_fold.svelte';

	import Add from './add.svelte';

	export let data;
	let { categories } = data;
	let { items } = data;
	let { total_page } = data;

	let bar_items = [
		{ name: 'live', icon: 'none' },
		{ name: 'draft', icon: 'none' },
		{ name: 'delete', icon: 'none' }
	];

	let open = false;

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

<Card>
	<Title title="Shop">
		<Button_Fold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</Title>

	<!-- <View
		show_view={open}
		on:ok={() => {
			open = false;
			submit();
		}}
	/> -->

	<!-- <Search
		on:ok={() => {
			pagination.init();
			submit();
		}}
	/> -->

	{#if $user && $user.roles.includes('admin')}
		<Status
			{bar_items}
			on:ok={() => {
				pagination.init();
				submit();
			}}
		>
			<svelte:fragment slot="after">
				<Button
					icon="add"
					icon_size="12"
					name="Add"
					class="tiny primary"
					on:click={() => {
						$module = {
							module: Add
						};
					}}
				/>
			</svelte:fragment>
		</Status>
	{/if}

	<Status
		on:ok={() => {
			pagination.init();
			submit();
		}}
	>
		<svelte:fragment slot="before">
			<Button
				name="all"
				class="tag"
				active={!$state.shop.category}
				on:click={() => {
					$state.shop.category = '';
					pagination.init();
					submit();
				}}
			/>
			{#each categories as category}
				<Button
					name={category.name}
					class="tag"
					active={$state.shop.category == category.name}
					on:click={() => {
						$state.shop.category = category.name;
						pagination.init();
						submit();
					}}
				/>
			{/each}
		</svelte:fragment>
	</Status>

	<Body grid={$user.setting.item_view != 'list'}>
		{#each items as item (item.key)}
			<Item {item} view_list={$user.setting.item_view == 'list'} />
		{:else}
			no item here
		{/each}
	</Body>

	<!-- <svelte:component
		this={Pagination}
		bind:this={pagination}
		{total_page}
		on:ok={() => {
			submit();
		}}
	/> -->
</Card>
