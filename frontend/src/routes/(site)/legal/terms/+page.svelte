<script>
	import { Content, PageTitle, TOC, TOCList } from '$lib/layout';
	import { Datetime, Marked, SideMenu } from '$lib/macro';
	import Contact from '../../contact/contact.svelte';
	import { content } from './text';

	let menu = $state();
</script>

<!-- TODO: review text -->
<!-- TODO: review all email template -->

<PageTitle>
	{#snippet title()}
		Terms & Conditions
	{/snippet}
	{#snippet copy()}
		The rules and guidelines for using Meji — outlining your rights, responsibilities, and how our
		platform works.
	{/snippet}
</PageTitle>

{#snippet nav()}
	<TOC>
		<TOCList container=".margdown_content" tag="h3" onclick={() => menu.onclick()}></TOCList>
	</TOC>
{/snippet}

<Content --content-width="calc(var(--mobileWidth))">
	<div class="block">
		<div class="nav">
			{@render nav()}
		</div>

		<div>
			<div class="date">
				<em> Last Updated: </em>
				<Datetime datetime="20 mar 2026"></Datetime>
			</div>

			<div class="margdown_content">
				<Marked {content}></Marked>
			</div>
			<Contact></Contact>
		</div>
	</div>

	<SideMenu bind:this={menu} --side_menu-bottom="calc(var(--headerHeight2) + 1px)">
		{@render nav()}
	</SideMenu>
</Content>

<style>
	.block {
		display: flex;
		gap: 16px;
	}

	.date {
		font-size: 0.7rem;
	}

	.nav {
		display: none;
		flex-shrink: 0;

		@media screen and (min-width: 600px) {
			display: block;
			width: 200px;
		}
	}
</style>
