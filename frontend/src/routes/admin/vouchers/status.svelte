<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, module, set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Add from './_add.svelte';

	export let page_name = '';
	let status = 'all';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			status = params.get('status');
		}
	});

	let statuses = ['all', 'inactive', 'unused', 'used'];
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<div class="left">
			{#each statuses as s}
				<Button
					name={s}
					class="tiny"
					active={status == s}
					on:click={() => {
						status = s;
						set_state(page_name, 'status', s != 'all' ? s : '');
					}}
				/>
			{/each}
		</div>

		<Button
			icon="add"
			icon_size="12"
			name="Add"
			class="tiny primary"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		/>
	</div>
{/if}

<style>
	.block,
	.left {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
	.block {
		justify-content: space-between;
		margin-top: var(--sp2);
	}
</style>
