<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { goto } from '$app/navigation';
	import { user, module, loading, portal, state } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from './tag_form.svelte';
	import Tag from '$lib/button.tag.svelte';
	import { onMount } from 'svelte';

	export let item = {};
	export let edit_mode = false;
	export let all_tags;
	let open = true;

	onMount(() => {
		$portal = {
			type: 'tag',
			data: {
				loaded: false,
				data: []
			}
		};
	});
</script>

<div class="horizontal main">
	{#if open}
		<div
			class="horizontal tags"
			transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
		>
			{#each item.tags as tag}
				<Tag
					no_grow
					on:click={() => {
						let i = $state.findIndex((x) => x.name == 'shop');
						if (i != -1) {
							$state[i].loaded = false;
						}

						$loading = 'loading . . .';
						goto(`/shop?${new URLSearchParams({ tag }).toString()}`);
					}}
				>
					{tag}
				</Tag>
			{:else}
				{#if edit_mode && $user.permissions.includes('item:edit_tag')}
					No Tag
				{/if}
			{/each}
		</div>
	{/if}

	<!-- <ButtonFold
		{open}
		on:click={() => {
			open = !open;
		}}
	/> -->
	{#if edit_mode && $user.permissions.includes('item:edit_tag')}
		<Button
			class="round"
			on:click={() => {
				$module = {
					module: Form,
					item,
					all_tags
				};
			}}
			tooltip="Edit tag"
		>
			<SVG type="edit" size="10" />
		</Button>
	{/if}
</div>

<style>
	.horizontal {
		display: flex;
		gap: var(--sp1);
	}

	.main {
		align-items: center;
		justify-content: space-between;
	}

	.tags {
		flex-wrap: wrap;
	}
</style>
