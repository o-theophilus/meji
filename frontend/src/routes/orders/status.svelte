<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state, user } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name = '';
	let status = 'ordered';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			status = params.get('status');
		}
	});

	let states = ['pending', 'ordered', 'processing', 'enroute', 'delivered', 'canceled'];
</script>

<div class="block">
	<div class="left">
		{#each states as s}
			<Button
				class="small {status == s ? 'primary' : ''}"
				on:click={() => {
					status = s;
					set_state(page_name, 'status', s != 'ordered' ? s : '');
				}}
			>
				{s}
			</Button>
		{/each}
	</div>

	{#if $user.roles.includes('admin')}
		<Button
			class="small {$page.url.searchParams.has('admin') ? 'primary' : ''}"
			on:click={() => {
				if ($page.url.searchParams.has('admin')) {
					set_state(page_name, 'admin', '');
				} else {
					set_state(page_name, 'admin', 'true');
				}
			}}
		>
			Admin: {$page.url.searchParams.has('admin') ? 'On' : 'Off'}
		</Button>
	{/if}
</div>

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
