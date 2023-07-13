<script context="module">
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';
	import { get_query } from '$lib/page_state.js';

	export async function load({ fetch, session }) {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user${get_query('users')}`, {
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

						users: resp.data.users,
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
</script>

<script>
	import { token } from '$lib/cookie.js';
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	import Search from '$lib/comp/search.svelte';
	import Status from '$lib/comp/status_bar.svelte';
	import View from '$lib/comp/page_view.svelte';
	import Pagination from '$lib/comp/pagination.svelte';
	import Button_Fold from '$lib/comp/button_fold.svelte';

	import User from './user.svelte';

	export let user;
	$: user = $user ? $user : user;

	export let users = [];
	export let total_page = 1;

	let open = false;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user${get_query('users')}`, {
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
				users = resp.data.users;
				total_page = resp.data.total_page;
			} else {
				error = resp.message;
			}
		}
	};

	let pagination;
	let bar_items = [
		{ name: 'confirm', icon: 'none' },
		{ name: 'anonymous', icon: 'none' },
		{ name: 'block', icon: 'none' },
		{ name: 'delete', icon: 'none' },
		{ name: 'report', icon: 'none' }
	];
</script>

<svelte:head>
	<title>Users | Meji</title>
</svelte:head>

<Card>
	<Title title="Users">
		<Button_Fold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</Title>

	<View
		show_view={open}
		on:ok={() => {
			open = false;
			submit();
		}}
	/>

	<Search
		on:ok={() => {
			pagination.init();
			submit();
		}}
	/>

	<Status
		{bar_items}
		on:ok={() => {
			pagination.init();
			submit();
		}}
	/>
	<Body>
		{#each users as user (user.key)}
			<User {user} />
		{:else}
			no user here
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
