<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, page_state } from '$lib/store.svelte.js';

	import { Hero, Tags, About } from './_home';
	import { Meta, Log } from '$lib/macro';
	import { Dialogue } from '$lib/info';
	import { Login } from '$lib/auth';
	import { Content } from '$lib/layout';
	import { LinkArrow } from '$lib/button';
	import ItemGroup from './shop/item_group.svelte';

	let { data } = $props();
	let new_arrivals = $derived(data.new_arrivals);
	let discount = $derived(data.discount);

	const get_module = (x) => {
		if (x == 'login') {
			return Login;
		} else if (x == 'dialogue') {
			return Dialogue;
		}
		return null;
	};

	onMount(() => {
		let _module = null;
		let value = {};

		for (const [key, val] of page.url.searchParams.entries()) {
			if (key == 'module') {
				_module = get_module(val);
			} else {
				value[key] = val;
			}
		}

		if (_module) {
			module.open(_module, value);
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Log entity_type={'page'} />
<Meta
	title="Home"
	description="Meji is your No. 1 trusted online shopping destination in Nigeria."
/>

<Hero />
<!-- <Advert space="home_1" placeholder /> -->
<Tags />

<Content --content-width="1200px" --content-height="100%">
	<ItemGroup id="new_arrivals" items={new_arrivals}>
		{#snippet _title()}
			<div class="a">
				New Arrivals
				<LinkArrow
					onclick={() => page_state.goto('shop', { order: 'latest' })}
					--link-font-size="0.8rem">See All</LinkArrow
				>
			</div>
		{/snippet}
	</ItemGroup>
	<ItemGroup id="discount" items={discount}>
		{#snippet _title()}
			<div class="a">
				Discounted Items
				<LinkArrow
					onclick={() => page_state.goto('shop', { order: 'discount' })}
					--link-font-size="0.8rem">See All</LinkArrow
				>
			</div>
		{/snippet}
	</ItemGroup>
	<About></About>
</Content>

<style>
	.a {
		display: flex;
		flex-direction: column;
	}
</style>
