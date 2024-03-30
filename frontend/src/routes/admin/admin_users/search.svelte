<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user as _user, set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';

	export let page_name;

	// #TODO: get from backend
	let actions = {
		all: ['all'],
		admin: ['all', 'manage_photo'],
		user: ['all', 'view', 'view_balance', 'set_role'],
		item: [
			'all',
			'add',
			'advert',
			'edit_status',
			'edit_name',
			'edit_tag',
			'edit_price',
			'edit_info',
			'edit_variation'
		],
		voucher: ['all', 'view', 'add', 'view_code'],
		log: ['all', 'view']
	};

	let user = '';
	let type = 'all';
	let role = 'all';
	$: search = `${user || 'all'}:${type || 'all'}:${role || 'all'}`;

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			let temp = params.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				user = temp[0] != 'all' ? temp[0] : '';
				type = temp[1];
				role = temp[2];
			}
		}
	});
</script>

<section>
	<div class="line">
		<select
			bind:value={type}
			on:input={() => {
				role = 'all';
			}}
		>
			{#each Object.entries(actions) as [type, action]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={role}>
			{#each actions[type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>

	<div class="line">
		<Search
			placeholder="Search for User"
			bind:search={user}
			on:clear={() => {
				user = '';
			}}
		/>
		<Button
			class="primary"
			on:click={() => {
				if (search == 'all:all:all') {
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
