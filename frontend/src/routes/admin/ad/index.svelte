<script context="module">
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';
	import { get_query } from '$lib/page_state.js';

	export async function load({ fetch, session }) {
		if (session.user.roles.includes('admin')) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}ads${get_query('ad')}`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							user: session.user,

							items: resp.data.items,
							total_page: resp.data.total_page
						}
					};
				} else {
					return {
						status: 404,
						error: resp.message
					};
				}
			}
		}
		return {
			status: 404,
			error: 'Unauthorised Access'
		};
	}
</script>

<script>
	import { token } from '$lib/cookie.js';
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from './_item.svelte';

	import Search from '$lib/comp/search.svelte';
	import Pagination from '$lib/comp/pagination.svelte';

	export let user;
	$: user = $user ? $user : user;

	export let items = [];
	export let total_page = 1;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}ads${get_query('ad')}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

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

<svelte:head>
	<title>Shop | Meji</title>
</svelte:head>

<Card>
	<Title title="Shop" />

	<Search
		on:ok={() => {
			pagination.init();
			submit();
		}}
	/>

	<Body>
		{#each items as item (item.key)}
			<Item {item} />
		{:else}
			no item here
		{/each}
	</Body>

	<svelte:component
		this={Pagination}
		bind:this={pagination}
		{total_page}
		on:ok={(e) => {
			submit();
		}}
	/>
</Card>
