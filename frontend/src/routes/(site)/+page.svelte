<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { Login } from '$lib/auth';
	import { Button, LinkArrow } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Content, PageTitle } from '$lib/layout';
	import { Log, Meta, ToTop } from '$lib/macro';
	import { module, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { About, Advert, CTA, FAQ, Hero, ItemGroup, ItemGroup2, Tags, Testimonial } from './_home';

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
			replaceState('/');
		}
	});
</script>

<Log entity_type={'page'} />
<Meta
	title="Home"
	description="Meji is your No. 1 trusted online shopping destination in Nigeria."
/>

<Content>
	<PageTitle>
		{#snippet title()}
			Shopping, refined.
		{/snippet}
		{#snippet copy()}
			Discover products selected for their quality, design, and everyday usefulness.

			<br />
			<br />

			<Button
				--button-background-color="var(--cl1)"
				--button-color="white"
				--button-outline-color="transparent"
				href="/shop"
				icon2="arrow-right"
			>
				Shop Now
			</Button>
		{/snippet}
	</PageTitle>

	<Hero />
	<Advert space="home_1" --advert-margin-bottom="80px" />
	<Tags />

	<ItemGroup id="new_arrivals" items={new_arrivals}>
		{#snippet _title()}
			<div class="page_title">New Arrivals</div>
			<LinkArrow
				onclick={() => page_state.goto('shop', { order: 'latest' })}
				--link-font-size="0.8rem">See All</LinkArrow
			>
		{/snippet}
	</ItemGroup>

	<ItemGroup2 id="discount" items={discount}>
		{#snippet _title()}
			<div class="page_title">Discounted Items</div>
			<LinkArrow
				onclick={() => page_state.goto('shop', { order: 'discount' })}
				--link-font-size="0.8rem">See All</LinkArrow
			>
		{/snippet}
	</ItemGroup2>

	<About></About>
	<Testimonial></Testimonial>
	<FAQ></FAQ>
	<CTA></CTA>
	<ToTop />
</Content>
