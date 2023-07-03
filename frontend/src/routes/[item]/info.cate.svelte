<script>
	import { goto } from '$app/navigation';
	import { state } from '$lib/page_state.js';
	import { user, module } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';

	import Category from './_category.svelte';

	export let item
</script>

{#if item.categories.length > 0 || ($user && $user.roles.includes('admin'))}
	<div class="categories">
		{#each item.categories as category}
			<Button
				name={category}
				class="tag"
				on:click={() => {
					$state['shop'].search = '';
					$state['shop'].category = category;
					$state['shop'].page_no = 1;

					goto('/shop');
				}}
			/>
		{/each}
		{#if $user && $user.roles.includes('admin')}
			<Button
				icon="edit"
				icon_size="12"
				class="tiny"
				on:click={() => {
					$module = {
						module: Category,
						data: {
							item
						}
					};
				}}
				tooltip="Edit Item Category"
			/>
		{/if}
	</div>
{/if}

<style>
	.categories {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--gap1);
	}
</style>
