<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let page_name = '';
	let action = 'all';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('action')) {
			action = params.get('action');
		}
	});

	let actions = [
		'all',
		'view_item',
		'pending',
		'change_delivery_date',
		'ordered',
		'changed_order_status',
		'created_voucher',
		'changed_voucher_status',
		'used_voucher'
	];
</script>

<div class="block">
	{#each actions as s}
		<Button
			name={s}
			class="tiny"
			active={action == s}
			on:click={() => {
				action = s;
				set_state(page_name, 'action', s != 'all' ? s : '');
			}}
		/>
	{/each}
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;

		margin-top: var(--sp2);
	}
</style>
