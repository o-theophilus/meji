<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;

	let page_name = 'users';
</script>

<Meta title="Users" description="Users" />

<Card>
	<b> User{users.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each users as x}
		{x.key}
		<br />
		{x.name}
		<br />
		{x.email}
		<br />
		{x.phone}
		<br />
		<!-- {x.address}
		<br /> -->
		{x.photo}
		<br />
		<br />
	{:else}
		no item here
	{/each}
	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
