<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import UpdateUrl from '$lib/update_url.svelte';
	import Card from '$lib/card.svelte';
	import Back from '$lib/button/back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from './user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { user_status } = data;
</script>

<UpdateUrl />
<Meta title="All Users" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>

		User{users.length > 1 ? 's' : ''}

		<svelte:fragment slot="right">
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<Status array={['all', ...user_status]} default_value="all" />
	<br />
	<Search />

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} card />
</Card>

<style>
</style>
