<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state, user } from '$lib/store.js';

	import Button from '$lib/button.svelte';

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
	{#each states as s}
		<Button
			class="small {status == s ? 'primary' : ''}"
			on:click={() => {
				status = s;
				set_state(page_name, 'status', s != 'ordered' ? s : '');
			}}
		>
			<span>
				{s}
			</span>
		</Button>
	{/each}

	{#if $user.roles.includes('admin')}
		<div class="right">
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
		</div>
	{/if}
</div>

<style>
	.block {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: var(--sp1);

		margin-top: var(--sp2);
	}
	.right {
		margin-left: auto;
	}

	span {
		text-transform: capitalize;
	}
</style>
