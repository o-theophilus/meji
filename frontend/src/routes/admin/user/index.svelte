<script>
	import { token } from '$lib/cookie.js';
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';

	import Search from '$lib/comp/search.svelte';
	import Status from '$lib/comp/status_bar.svelte';
	import View from '$lib/comp/page_view.svelte';
	import Pagination from '$lib/comp/pagination.svelte';
	import ButtonFold from '$lib/comp/button.fold.svelte';

	import User from './user.svelte';

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
	<b>Users</b>
	<ButtonFold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
	<br />
	<br />
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

	{#each users as user (user.key)}
		<User {user} />
	{:else}
		no user here
	{/each}

	<svelte:component
		this={Pagination}
		bind:this={pagination}
		{total_page}
		on:ok={(e) => {
			submit();
		}}
	/>
</Card>
