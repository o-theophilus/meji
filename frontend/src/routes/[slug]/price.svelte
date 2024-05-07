<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Info from './price.info.svelte';
	import Discount from './price.discount.svelte';
	import Form from './price_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open_discount = false;
</script>

<div class="row space v_margin">
	<Info {item} />

	<div class="row">
		{#if item.old_price}
			<BRound
				icon="info"
				size="8"
				on:click={() => {
					open_discount = !open_discount;
				}}
			/>
		{/if}
		{#if edit_mode && $user.permissions.includes('item:edit_price')}
			<BRound
				icon="edit"
				size="10"
				tooltip="Edit Price"
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
			/>
		{/if}
	</div>
</div>

{#if item.old_price && open_discount}
	<div class="v_margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<Discount {item} />
	</div>
{/if}

<style>
	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.space {
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}
</style>
