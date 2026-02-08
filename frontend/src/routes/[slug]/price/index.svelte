<script>
	import { module, app } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import { Icon } from '$lib/macro';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';
	import Price from './price.svelte';
	import Info from './info.svelte';

	let { item, edit_mode, update } = $props();

	let show_discount = $state(false);
</script>

<div class="comp">
	{#if app.user.access.includes('item:edit_price') && edit_mode}
		<Edit_Button
			onclick={() =>
				module.open(Form, {
					key: item.key,
					price: item.price,
					price_old: item.price_old,
					update
				})}
		>
			Edit Price
		</Edit_Button>
	{/if}

	<Price {item}>
		<button onclick={() => (show_discount = !show_discount)}>
			<Icon icon="info"></Icon>
		</button>
	</Price>

	{#if show_discount}
		<div transition:slide>
			<Info {item}></Info>
		</div>
	{/if}
</div>

<style>
	.comp {
		margin-top: 24px;
	}

	button {
		all: unset;
		cursor: pointer;

		display: flex;
		transition: color 0.2s ease-in-out;

		&:hover {
			color: var(--ft1);
		}
	}
</style>
