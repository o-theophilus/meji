<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import UpdateUrl from '$lib/update_url.svelte';
	import Card from '$lib/card.svelte';
	import Back from '$lib/button.back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from './user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import OrderBy from '$lib/order_by.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;
	let { user_status } = data;
</script>

<UpdateUrl />
<Meta title="All Users" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			User{users.length > 1 ? 's' : ''}
		</div>

		<OrderBy {page_name} {order_by} />
	</div>
</Center>

<Card>
	<Status {page_name} array={['all', ...user_status]} default_value="all" />
	<br />
	<Search {page_name} />
	<br />

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
