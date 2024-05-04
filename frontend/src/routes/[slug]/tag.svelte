<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { goto } from '$app/navigation';
	import { user, module, loading, portal, state } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from './tag_form.svelte';
	import Tag from '$lib/button/tag.svelte';
	import { onMount } from 'svelte';

	export let item = {};
	export let edit_mode = false;
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
						let pn = 'shop';
						let i = $state.findIndex((x) => x.name == pn);
						if (i != -1) {
							$state.splice(i, 1);
						}

						$state.push({
							name: pn,
							search: `?${new URLSearchParams({ tag }).toString()}`,
							data: [],
							loaded: false
						});

						$loading = 'loading . . .';
						goto('/shop');
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
		<BRound
			on:click={() => {
				$module = {
					module: Form,
					item
				};
			}}
			tooltip="Edit tag"
		>
			<SVG type="edit" size="10" />
		</BRound>
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
