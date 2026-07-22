<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { Login } from '$lib/auth';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Content, PageTitle } from '$lib/layout';
	import { Log, Meta, ToTop } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { About, Advert, CTA, FAQ, Hero, ItemGroup, Tags, Testimonial } from './_home';

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

<Meta
	title="Home"
	description="Meji is your No. 1 trusted online shopping destination in Nigeria."
/>
<Log entity_type="page" />

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
				--button-background-color="var(--cl3)"
				--button-background-color-hover="var(--cl3_)"
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
	<Advert space="home_1" --advert-margin-top="80px" --advert-margin-bottom="80px" />
	<Tags />
	<ItemGroup></ItemGroup>
	<About></About>
	<Testimonial></Testimonial>
	<FAQ></FAQ>
	<CTA></CTA>
	<ToTop />
</Content>
