<script>
	import { Content, PageTitle } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import Contact from '../contact/contact.svelte';
	import { faqs } from './faq';
	import Group from './group.svelte';

	let ops = $state({ open: null });
</script>

<Meta title="FAQ" description="Need quick answers? Find solutions to common questions below." />
<Log entity_type={'page'} />


<Content>
	<PageTitle>
		{#snippet title()}
			Frequently Asked Questions
		{/snippet}
		{#snippet copy()}
			Need quick answers? Find solutions to common questions below.
		{/snippet}
	</PageTitle>
	
	{#each faqs as x}
		<div class="categoty">
			{x.category}
		</div>

		<Group bind:ops category={x}></Group>
	{/each}
	<Contact></Contact>
</Content>

<style>
	.categoty {
		margin-top: 52px;
		font-weight: 1.2rem;
		font-weight: 800;
	}
</style>
