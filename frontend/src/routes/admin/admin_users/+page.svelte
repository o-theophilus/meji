<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Card from '$lib/card.svelte';
	import Back from '$lib/button/back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from '../users/user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import Search from './search.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { permissions } = data;
	let { order_by } = data;
</script>

<UpdateUrl />
<Meta title="Users" description="Users with elevated permission." />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			User{users.length > 1 ? 's' : ''}
		</div>
		<OrderBy {order_by} />
	</div>
</Center>

<Card>
	<Search {permissions} />

	<br />
	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</Card>

<style>
</style>
