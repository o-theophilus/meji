<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button.fold.svelte';

	export let data;
	let { unused } = data;
	let { users } = data;
	let { items } = data;
	let { adverts } = data;

	let open_unused = unused.length > 0;
	let open_users = users.length > 0;
	let open_items = items.length > 0;
	let open_adverts = adverts.length > 0;
</script>

<Meta title="Admin Dashboard" description="Admin Dashboard" />

<Center>
	<br />
	<div class="ctitle">Manage Photos</div>
</Center>

<Card>
	<div class="title">
		Unused Photos ({unused.length})
		<ButtonFold
			open={open_unused}
			on:click={() => {
				open_unused = !open_unused;
			}}
		/>
	</div>

	{#if open_unused}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<br />
			{#each unused as x}
				<img
					src={`${x}/100` || '/image/item.png'}
					alt="missing"
					onerror="this.src='/image/item.png'"
				/>
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<Card>
	<div class="title">
		Users with missing Photos ({users.length})
		<ButtonFold
			open={open_users}
			on:click={() => {
				open_users = !open_users;
			}}
		/>
	</div>

	{#if open_users}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<br />
			{#each users as x}
				<a href="/profile?user={x.key}">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<Card>
	<div class="title">
		Items with missing Photos ({items.length})
		<ButtonFold
			open={open_items}
			on:click={() => {
				open_items = !open_items;
			}}
		/>
	</div>

	{#if open_items}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<br />
			{#each items as x}
				<a href="/{x.key}">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<Card>
	<div class="title">
		Adverts with missing photos ({adverts.length})
		<ButtonFold
			open={open_adverts}
			on:click={() => {
				open_adverts = !open_adverts;
			}}
		/>
	</div>

	{#if open_adverts}
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<br />
			{#each adverts as x}
				<a href="/{x.key}?edit=true&advert=true">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
