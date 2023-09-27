<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, module, set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';

	export let page_name = '';
	let status = 'live';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			status = params.get('status');
		}
	});
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<div class="left">
			{#each ['live', 'draft', 'delete'] as s}
				<Button
					class="small {status == s ? 'primary' : ''}"
					on:click={() => {
						status = s;
						set_state(page_name, 'status', s != 'live' ? s : '');
					}}
				>
					{s}
				</Button>
			{/each}
		</div>

		<Button
			class="small primary"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		>
			<SVG type="add" size="12" />
			Add
		</Button>
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
