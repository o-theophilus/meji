<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	export let search_query;

	let user_key = '';
	let entity_type = 'all';
	let action = 'all';
	let entity_key = '';
	let search = `${user_key}:${entity_type}:${action}:${entity_key}`;

	export const set_value = ({ u = '', e = '' }) => {
		user_key = u || user_key;
		entity_key = e || entity_key;
	};

	onMount(() => {
		if ($page.url.searchParams.has('search')) {
			let temp = $page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 4) {
				user_key = temp[0];
				entity_type = temp[1];
				action = temp[2];
				entity_key = temp[3];
				search = `${user_key}:${entity_type}:${action}:${entity_key}`;
			}
		}
	});

	const submit = (clear = false) => {
		if (clear) {
			user_key = '';
			entity_type = 'all';
			action = 'all';
			entity_key = '';
		}

		let check = `${search}`;
		search = `${user_key}:${entity_type || 'all'}:${action || 'all'}:${entity_key}`;
		if (search != check) {
			set_state('search', search != ':all:all:' ? search : '');
		}
	};
</script>

<section>
	{#if $user.permissions.includes('log:view')}
		<div class="line">
			<Search
				non_default
				placeholder="Search for User"
				bind:search={user_key}
				on:clear={() => {
					user_key = '';
				}}
			/>
			<Button
				on:click={() => {
					set_value({ u: $user.key });
				}}
			>
				Me
			</Button>
		</div>
	{/if}

	<div class="line">
		<select
			bind:value={entity_type}
			on:input={() => {
				action = 'all';
			}}
		>
			{#each Object.entries(search_query) as [type, _]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={action}>
			{#each search_query[entity_type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>
	<div class="line">
		<Search
			non_default
			placeholder="Search for {entity_type}"
			bind:search={entity_key}
			on:clear={() => {
				entity_key = '';
			}}
		/>
		<BRound
			disabled={`${user_key}:${entity_type}:${action}:${entity_key}` == search}
			on:click={() => {
				submit();
			}}
		>
			<SVG type="search" size="12" />
		</BRound>
		<BRound
			extra="hover_red"
			disabled={`${user_key}:${entity_type}:${action}:${entity_key}` == ':all:all:'}
			on:click={() => {
				submit(true);
			}}
		>
			<SVG type="close" size="8" />
		</BRound>
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
