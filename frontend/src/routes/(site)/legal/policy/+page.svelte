<script>
	import { Tag } from '$lib/button';
	import { Content, PageTitle, TOC, TOCList } from '$lib/layout';
	import { Datetime, Icon, Log, Marked, Meta, SideMenu } from '$lib/macro';
	import Contact from '../../contact/contact.svelte';
	import { cookiesPolicy, privacyPolicy } from './text';
</script>

<!-- TODO: review text -->

<Log entity_type={'page'} />
<Meta title="Policy" description="How we collect, use, and protect your information." />

<PageTitle>
	{#snippet title()}
		Privacy & Data Policy
	{/snippet}
	{#snippet copy()}
		How we collect, use, and protect your information — including how cookies and tracking
		technologies work on Meji.
	{/snippet}
</PageTitle>

{#snippet nav()}
	<TOC>
		<a href="#privacyPolicy" class="sub_title" onclick={() => menu.onclick()}>Privacy Policy</a>
		<TOCList container=".privacyPolicy " tag="h3" onclick={() => menu.onclick()}></TOCList>

		<a href="#cookiesPolicy" class="sub_title" onclick={() => menu.onclick()}>Cookies Policy</a>
		<TOCList container=".cookiesPolicy" tag="h3" onclick={() => menu.onclick()}></TOCList>
	</TOC>
{/snippet}

<Content --content-width="calc(var(--mobileWidth))">
	<div class="container">
		<div class="nav">
			{@render nav()}
		</div>

		<div>
			<div class="section_title" id="privacyPolicy">
				<Icon icon="shield-user" size="24"></Icon>
				Privacy Policy
			</div>
			<br />
			<Tag>
				<em> Last Updated: </em>
				<Datetime datetime="20 mar 2026"></Datetime>
			</Tag>

			<div class="privacyPolicy">
				<Marked content={privacyPolicy}></Marked>
			</div>
			<br />
			<br />
			<div class="section_title" id="cookiesPolicy">
				<Icon icon="cookie" size="24"></Icon>
				Cookies Policy
			</div>
			<br />
			<Tag>
				<em> Last Updated: </em>
				<Datetime datetime="20 mar 2026"></Datetime>
			</Tag>

			<div class="cookiesPolicy">
				<Marked content={cookiesPolicy}></Marked>
			</div>
			<Contact></Contact>
		</div>
	</div>

	<SideMenu bind:this={menu} --side_menu-bottom="calc(var(--headerHeight2) + 1px)">
		{@render nav()}
	</SideMenu>
</Content>

<style>
	.container {
		display: flex;
		gap: 16px;
	}

	.sub_title {
		display: inline-block;
		font-weight: 800;
		color: var(--ft1);
		text-decoration: none;

		&:hover {
			color: var(--cl1);
		}

		&:not(:first-child) {
			margin-top: 12px;
		}
	}

	.section_title {
		display: flex;
		align-items: center;
		gap: 16px;

		background-color: var(--bg2);
		padding: 16px;
		border-radius: 8px;
		font-size: 2rem;
		font-weight: 800;
		color: var(--ft1);
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
