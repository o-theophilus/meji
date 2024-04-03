<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Info from './price.info.svelte';
	import Discount from './price.discount.svelte';
	import Form from './price_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open_discount = false;
</script>

<div class="horizontal">
	<Info {item} />

	<div class="horizontal">
		{#if item.old_price}
			<Button
				class="round"
				on:click={() => {
					open_discount = !open_discount;
				}}
			>
				<SVG type="info" size="8" />
			</Button>
		{/if}
		{#if edit_mode && $user.permissions.includes('item:edit_price')}
			<Button
				class="round"
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
				tooltip="Edit Price"
			>
				<SVG type="edit" size="10" />
			</Button>
		{/if}
	</div>
</div>
{#if item.old_price && open_discount}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<Discount {item} />
	</div>
{/if}

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}
</style>
