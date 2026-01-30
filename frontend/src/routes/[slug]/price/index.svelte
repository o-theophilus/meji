<script>
	import { module, app } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import { Button } from '$lib/button';
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
		<Button
			icon="info"
			--button-padding-x="0"
			--button-width="18px"
			--button-height="18px"
			--button-border-radius="50%"
			--button-color="var(--ft2)"
			--button-background-color="var(--bg1)"
			onclick={() => {
				show_discount = !show_discount;
			}}
		></Button>
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
</style>
