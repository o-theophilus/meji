<script>
	// import marked from 'marked';

	export let md = '';

	// 	export let md = `
	// ---
	// # HEADERS
	// ---

	// # This is an \\<h1> tag
	// ## This is an \\<h2> tag
	// ### This is an \\<h3> tag
	// #### This is an \\<h4> tag
	// ##### This is an \\<h5> tag
	// ###### This is an \\<h6> tag

	// ---
	// # EMPHASIS
	// *This text will be italic*

	// **This text will be bold**

	// *You **can** combine them*

	// ---
	// # BLOCKQUOTES

	// > I’ve always been more interested
	// > in the future than in the past.

	// ---
	// # LISTS

	// * Item 1
	// * Item 2
	//    * Item 2a
	//    * Item 2b

	// 1. Item 1
	// 1. Item 2
	// 1. Item 3
	//    * Item 3a
	//    * Item 3b

	// ---
	// # IMAGES

	// ![GitHub Logo](/images/akropol_001.jpg)

	// ---
	// # LINKS

	// http://github.com - automatic!

	// or

	// [GitHub](http://github.com)

	// ---
	// # BACKSLASH ESCAPES

	// \\*literal asterisks*

	// ---
	// # FENCED CODE BLOCKS

	// \`\`\`javascript
	// function test() {
	// 	console.log("look ma’, no spaces");
	// \`\`\`

	// ---
	// # TASK LISTS

	// 1. [x] done
	// * [ ] undone

	// ---
	// # TABLES

	// First Header | Second Header
	// ------------ | -------------
	// Content cell 1 | Content cell 2
	// Content column 1 | Content column 2

	// 	`;
</script>

<div class="marked">
	{@html md}
</div>

<style>
	* {
		text-align: justify;
	}

	:global(.marked ul, .marked ol) {
		padding-left: 1rem;
	}
	:global(.marked p, .marked ul, .marked ol, h1, h2, h3, h4, h5, h6) {
		margin: 1rem 0;
	}
	:global(.marked * ol, .marked * ul) {
		margin: 0;
		padding-left: 2rem;
	}

	:global(.marked hr) {
		border: none;
		border-top: 2px solid var(--ac5);
	}
	:global(.marked > :first-child) {
		margin-top: 0;
	}
	:global(.marked > :last-child) {
		margin-bottom: 0;
	}

	/* costom */
	:global(.marked .column) {
		display: grid;
		gap: var(--sp1);
	}
	:global(.marked .row) {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
	}
</style>
