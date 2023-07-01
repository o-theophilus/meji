<script>
	import { user, module } from '$lib/store.js';

	import Body from '$lib/comp/card_body.svelte';
	import Price from './info_price.svelte';
	import Rating from './info_rating.svelte';
	import Cate from './info_cate.svelte';
	import Save from '$lib/comp/item_save.svelte';
	import Button from '$lib/comp/button.svelte';

	import Edit from './_edit.svelte';
	import Status from './_status.svelte';
	import Variation from './_variation_options.svelte';

	export let item = {};

	$: if ($user) {
		item.save = false;
		for (const i in $user.saves) {
			if ($user.saves[i].key == item.key) {
				item.save = true;
				break;
			}
		}
	}
</script>

<Body>
	<div class="name h">
		{item.name}
		{#if $user && $user.roles.includes('admin')}
			<Button
				icon="edit"
				class="tiny"
				icon_size="12"
				on:click={() => {
					$module = {
						module: Edit,
						data: {
							item
						}
					};
				}}
				tooltip="Edit Details"
			/>

			<Button
				icon="logo"
				class="tiny"
				icon_size="12"
				on:click={() => {
					$module = {
						module: Variation,
						data: {
							item
						}
					};
				}}
				tooltip="Edit Variation"
			/>
		{/if}
		<div class="save">
			<Save {item} />
		</div>
	</div>

	{#if $user && $user.roles.includes('admin')}
		<div class="h">
			Status: {item.status}
			<Button
				icon="edit"
				class="tiny"
				icon_size="12"
				on:click={() => {
					$module = {
						module: Status,
						data: {
							item
						}
					};
				}}
				tooltip="Edit Status"
			/>
		</div>
	{/if}

	<Cate {item} />
	<Price {item} />
	<Rating {item} />
</Body>

<style>
	.name {
		position: relative;

		font-weight: 500;
	}

	.save {
		position: absolute;
		right: 0;
		top: 0;
	}

	@media screen and (min-width: 800px) {
	}
</style>
