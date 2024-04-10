<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;
	export let permissions;

	let user_key = '';
	let type = 'all';
	let action = 'all';
	let search = `${user_key}:${type}:${action}`;

	onMount(() => {
		if ($page.url.searchParams.has('search')) {
			let temp = $page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				user_key = temp[0];
				type = temp[1];
				action = temp[2];
				search = `${user_key}:${type}:${action}`;
			}
		}
	});

	const submit = (clear = false) => {
		if (clear) {
			user_key = '';
			type = 'all';
			action = 'all';
		}

		let check = `${search}`;
		search = `${user_key}:${type || 'all'}:${action || 'all'}`;
		if (search != check) {
			set_state(page_name, 'search', search != ':all:all' ? search : '');
		}
	};
</script>

<section>
	<div class="line">
		<select
			bind:value={type}
			on:input={() => {
				action = 'all';
			}}
		>
			{#each Object.entries(permissions) as [type, _]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={action}>
			{#each permissions[type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>

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
			class="round"
			disabled={`${user_key}:${type}:${action}` == search}
			on:click={() => {
				submit();
			}}
		>
			<SVG type="search" size="12" />
		</Button>
		<Button
			class="round hover_red"
			disabled={`${user_key}:${type}:${action}` == ':all:all'}
			on:click={() => {
				submit(true);
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
