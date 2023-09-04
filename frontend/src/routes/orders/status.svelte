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
	<div class="left">
		{#each states as s}
			<Button
				name={s}
				class="tiny"
				active={status == s}
				on:click={() => {
					status = s;
					set_state(page_name, 'status', s != 'ordered' ? s : '');
				}}
			/>
		{/each}
	</div>

	{#if $user.roles.includes('admin')}
		<Button
			name="Admin: {$page.url.searchParams.has('admin') ? 'On' : 'Off'}"
			class="tiny {$page.url.searchParams.has('admin') ? 'primary' : ''}"
			icon="edit"
			icon_size="12"
			on:click={() => {
				if ($page.url.searchParams.has('admin')) {
					set_state(page_name, 'admin', '');
				} else {
					set_state(page_name, 'admin', 'true');
				}
			}}
		/>
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
