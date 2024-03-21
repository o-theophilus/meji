<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user as me, set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;

	let actions = {
		all: ['all']
	};

	let in_user = '';
	let in_type = 'all';
	let in_action = 'all';
	let in_entity = '';

	let snap = `${in_user}:${in_type}:${in_action}:${in_entity}`;

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/log/action`);
		resp = await resp.json();

		if (resp.status == 200) {
			actions = resp.actions;
		}

		let params = $page.url.searchParams;
		if (params.has('search')) {
			let temp = params.get('search');
			temp = temp.split(':');
			if (temp.length == 4) {
				in_user = temp[0] != 'all' ? temp[0] : '';
				in_type = temp[1];
				in_action = temp[2];
				in_entity = temp[3] != 'all' ? temp[3] : '';

				snap = `${in_user}:${in_type}:${in_action}:${in_entity}`;
			}
		}
	});

	const set_search = (user = '', type = 'all', action = 'all', entity = '') => {
		if (user == 'all') {
			user = '';
			in_user = '';
		}
		if (entity == 'all') {
			entity = '';
			in_entity = '';
		}

		let search = `${user || 'all'}:${type || 'all'}:${action || 'all'}:${entity || 'all'}`;
		if (search == 'all:all:all:all') {
			search = '';
		}

		set_state(page_name, 'search', search);
		snap = `${user}:${type}:${action}:${entity}`;
	};

	export const set_value = ({ user = '', type = 'all', action = 'all', entity = '' }) => {
		if (user) {
			in_user = user;
		}
		if (type != 'all') {
			in_type = type;
		}
		if (action != 'all') {
			in_action = action;
		}
		if (entity) {
			in_entity = entity;
		}
	};
</script>

<section>
	{#if $me.roles.includes('log:view')}
		<div class="line">
			<Search
				placeholder="Search for User"
				bind:search={in_user}
				on:clear={() => {
					in_user = '';
				}}
			/>
			<Button
				class=""
				on:click={() => {
					set_value({ user: $me.key });
				}}
			>
				Me
			</Button>
		</div>
	{/if}

	<div class="line">
		<select
			bind:value={in_type}
			on:input={() => {
				in_action = 'all';
			}}
		>
			{#each Object.entries(actions) as [type, action]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={in_action}>
			{#each actions[in_type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>
	<div class="line">
		<Search
			placeholder="Search for {in_type}"
			bind:search={in_entity}
			on:clear={() => {
				in_entity = '';
			}}
		/>
		<Button
			class="round"
			disabled={`${in_user}:${in_type}:${in_action}:${in_entity}` == snap}
			on:click={() => {
				set_search(in_user, in_type, in_action, in_entity);
			}}
		>
			<SVG type="search" size="12" />
		</Button>
		<Button
			class="round hover_red"
			disabled={`${in_user}:${in_type}:${in_action}:${in_entity}` == ':all:all:'}
			on:click={() => {
				let reload = false;
				if (snap != ':all:all:') {
					reload = true;
				}

				in_user = '';
				in_type = 'all';
				in_action = 'all';
				in_entity = '';

				if (reload) {
					set_search();
				}
			}}
		>
			<SVG type="close" size="8" />
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
		align-items: center;
	}
</style>
