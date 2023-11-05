<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user as _user, set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';

	export let page_name;

	let actions = {
		all: ['all'],
		item: ['all', 'viewed', 'added_photo'],
		order: ['all', 'created', 'changed_delivery_date', 'changed_status', 'canceled'],
		voucher: ['all', 'created', 'activated', 'deactivated', 'used', 'deleted'],
		advert: ['all', 'created', 'added_photo', 'deleted']
	};

	let user = '';
	let type = 'all';
	let action = 'all';
	let entity = '';
	$: search = `${user || 'all'}:${type || 'all'}:${action || 'all'}:${entity || 'all'}`;

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			let temp = params.get('search');
			temp = temp.split(':');
			if (temp.length == 4) {
				user = temp[0] != 'all' ? temp[0] : '';
				type = temp[1];
				action = temp[2];
				entity = temp[3] != 'all' ? temp[3] : '';
			}
		}
	});
</script>

<section>
	{#if $_user.roles.includes('admin')}
		<div class="line">
			<Search
				placeholder="Search for User"
				bind:search={user}
				on:clear={() => {
					user = '';
				}}
			/>
			<Button
				class=""
				on:click={() => {
					user = $_user.key;
				}}
			>
				Mine
			</Button>
		</div>
	{/if}

	<div class="line">
		<select
			bind:value={type}
			on:input={() => {
				action = 'all';
			}}
		>
			{#each Object.entries(actions) as [type, action]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={action}>
			{#each actions[type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>
	<div class="line">
		<Search
			placeholder="Search for {type}"
			bind:search={entity}
			on:clear={() => {
				entity = '';
			}}
		/>
		<Button
			class="primary"
			on:click={() => {
				if (search == 'all:all:all:all') {
					search = '';
				}
				set_state(page_name, 'search', search);
			}}
		>
			Search
		</Button>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
