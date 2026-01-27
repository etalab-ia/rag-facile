import {Fragment,useCallback,useContext,useEffect,useRef} from "react"
import {Badge as RadixThemesBadge,Box as RadixThemesBox,Button as RadixThemesButton,Code as RadixThemesCode,Dialog as RadixThemesDialog,Flex as RadixThemesFlex,Heading as RadixThemesHeading,IconButton as RadixThemesIconButton,Link as RadixThemesLink,Separator as RadixThemesSeparator,Text as RadixThemesText,TextField as RadixThemesTextField,Theme as RadixThemesTheme,Tooltip as RadixThemesTooltip} from "@radix-ui/themes"
import {ColorModeContext,EventLoopContext,StateContexts} from "$/utils/context"
import {Info as LucideInfo,MessageSquarePlus as LucideMessageSquarePlus,MessagesSquare as LucideMessagesSquare,Trash as LucideTrash} from "lucide-react"
import {ReflexEvent,getRefValue,getRefValues,refs} from "$/utils/state"
import {Root as RadixFormRoot} from "@radix-ui/react-form"
import {Drawer as VaulDrawer} from "vaul"
import theme from "$/utils/theme"
import ReactMarkdown from "react-markdown"
import remarkMath from "remark-math"
import remarkGfm from "remark-gfm"
import rehypeKatex from "rehype-katex"
import "katex/dist/katex.min.css"
import rehypeRaw from "rehype-raw"
import rehypeUnwrapImages from "rehype-unwrap-images"
import {Link as ReactRouterLink} from "react-router"
import {PrismAsyncLight as SyntaxHighlighter} from "react-syntax-highlighter"
import oneLight from "react-syntax-highlighter/dist/esm/styles/prism/one-light"
import oneDark from "react-syntax-highlighter/dist/esm/styles/prism/one-dark"
import {jsx} from "@emotion/react"




function Badge_bc1564de00bf56a18cc809ef237fedde () {
  const reflex___state____state__reflex_chat___state____state = useContext(StateContexts.reflex___state____state__reflex_chat___state____state)



  return (
    jsx(RadixThemesBadge,{css:({ ["marginInlineEnd"] : "auto" }),size:"3",variant:"soft"},reflex___state____state__reflex_chat___state____state.current_chat_rx_state_,jsx(RadixThemesTooltip,{content:"The current selected chat."},jsx(LucideInfo,{size:14},)))
  )
}


function Root_5bed8eff1ccf63e2198e978821726120 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

    const handleSubmit_f3ede656e33801e2924148cd39971a62 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.reflex_chat___state____state.create_chat", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


  return (
    jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_f3ede656e33801e2924148cd39971a62},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"2",wrap:"wrap"},jsx(RadixThemesTextField.Root,{css:({ ["flex"] : "1", ["minWidth"] : "20ch" }),name:"new_chat_name",placeholder:"Chat name"},),jsx(RadixThemesButton,{},"Create chat")))
  )
}


function Dialog__root_55dde44f0a7bdd3058a1a49d59ddeaea () {
  const reflex___state____state__reflex_chat___state____state = useContext(StateContexts.reflex___state____state__reflex_chat___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_open_change_83ad850450380eb608dcea1bf09ebdd5 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflex_chat___state____state.set_is_modal_open", ({ ["is_open"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesDialog.Root,{onOpenChange:on_open_change_83ad850450380eb608dcea1bf09ebdd5,open:reflex___state____state__reflex_chat___state____state.is_modal_open_rx_state_},jsx(RadixThemesDialog.Trigger,{},jsx(RadixThemesIconButton,{css:({ ["padding"] : "6px" })},jsx(LucideMessageSquarePlus,{},))),jsx(RadixThemesDialog.Content,{css:({ ["backgroundColor"] : "var(--mauve-1)" })},jsx(Root_5bed8eff1ccf63e2198e978821726120,{},)))
  )
}


function Flex_20122bb049761b84fa7579d50fa6e001 () {
  const reflex___state____state__reflex_chat___state____state = useContext(StateContexts.reflex___state____state__reflex_chat___state____state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "stretch", ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesHeading,{css:({ ["color"] : "var(--mauve-11)" })},"Chats"),jsx(RadixThemesSeparator,{size:"4"},),Array.prototype.map.call(reflex___state____state__reflex_chat___state____state.chat_titles_rx_state_ ?? [],((chat_rx_state_,index_2fd921edd9d56ecb4a361ae74ec5705f)=>(jsx(VaulDrawer.Close,{asChild:true,key:chat_rx_state_},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(RadixThemesButton,{css:({ ["width"] : "80%" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_chat___state____state.set_chat", ({ ["chat_name"] : chat_rx_state_ }), ({  })))], [_e], ({  })))),variant:"surface"},chat_rx_state_),jsx(RadixThemesButton,{color:"red",css:({ ["width"] : "20%" }),variant:"surface"},jsx(LucideTrash,{css:({ ["strokeWidth"] : 1 }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflex_chat___state____state.delete_chat", ({ ["chat_name"] : chat_rx_state_ }), ({  })))], [_e], ({  }))))},))))))))
  )
}


        function ComponentMap_d59534cfa3df3086665270d8af3d1699 () {
            const { resolvedColorMode } = useContext(ColorModeContext)



            return (
                ({ ["h1"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h1",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"6",...props},children))), ["h2"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h2",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"5",...props},children))), ["h3"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h3",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"4",...props},children))), ["h4"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h4",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"3",...props},children))), ["h5"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h5",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"2",...props},children))), ["h6"] : (({node, children, ...props}) => (jsx(RadixThemesHeading,{as:"h6",css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),size:"1",...props},children))), ["p"] : (({node, children, ...props}) => (jsx(RadixThemesText,{as:"p",css:({ ["marginTop"] : "1em", ["marginBottom"] : "1em" }),...props},children))), ["ul"] : (({node, children, ...props}) => (jsx("ul",{css:({ ["listStyleType"] : "disc", ["marginTop"] : "1em", ["marginBottom"] : "1em", ["marginLeft"] : "1.5rem", ["direction"] : "column" }),...props},children))), ["ol"] : (({node, children, ...props}) => (jsx("ol",{css:({ ["listStyleType"] : "decimal", ["marginTop"] : "1em", ["marginBottom"] : "1em", ["marginLeft"] : "1.5rem", ["direction"] : "column" }),...props},children))), ["li"] : (({node, children, ...props}) => (jsx("li",{css:({ ["marginTop"] : "0.5em", ["marginBottom"] : "0.5em" }),...props},children))), ["a"] : (({node, children, ...props}) => (jsx(RadixThemesLink,{css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) }),href:"#",...props},children))), ["code"] : (({node, children, ...props}) => (jsx(RadixThemesCode,{...props},children))), ["pre"] : (({node, ...rest}) => { const {node: childNode, className, children: components, ...props} = rest.children.props; const children = String(Array.isArray(components) ? components.join('\n') : components).replace(/\n$/, ''); const match = (className || '').match(/language-(?<lang>.*)/); let _language = match ? match[1] : ''; ;             return jsx(SyntaxHighlighter,{children:children,css:({ ["marginTop"] : "1em", ["marginBottom"] : "1em" }),language:_language,style:((resolvedColorMode?.valueOf?.() === "light"?.valueOf?.()) ? oneLight : oneDark),wrapLongLines:true,...props},);         }) })
            )
        }
        

function Div_ae607de5d3e93df2d7764828faf96623 () {
  const ref_udaxihhe = useRef(null); refs["ref_udaxihhe"] = ref_udaxihhe;
const reflex___state____state__reflex_chat___state____state = useContext(StateContexts.reflex___state____state__reflex_chat___state____state)
const wasNearBottom_ref_udaxihhe = useRef(false);
const hadScrollbar_ref_udaxihhe = useRef(false);

const checkIfNearBottom_ref_udaxihhe = () => {
    if (!ref_udaxihhe.current) return;

    const container = ref_udaxihhe.current;
    const nearBottomThreshold = 50; // pixels from bottom to trigger auto-scroll

    const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight;

    wasNearBottom_ref_udaxihhe.current = distanceFromBottom <= nearBottomThreshold;

    // Track if container had a scrollbar
    hadScrollbar_ref_udaxihhe.current = container.scrollHeight > container.clientHeight;
};


const scrollToBottomIfNeeded_ref_udaxihhe = () => {
    if (!ref_udaxihhe.current) return;

    const container = ref_udaxihhe.current;
    const hasScrollbarNow = container.scrollHeight > container.clientHeight;

    // Scroll if:
    // 1. User was near bottom, OR
    // 2. Container didn't have scrollbar before but does now
    if (wasNearBottom_ref_udaxihhe.current || (!hadScrollbar_ref_udaxihhe.current && hasScrollbarNow)) {
      container.scrollTop = container.scrollHeight;
    }

    // Update scrollbar state for next check
    hadScrollbar_ref_udaxihhe.current = hasScrollbarNow;
};


useEffect(() => {
    const container = ref_udaxihhe.current;
    if (!container) return;

    scrollToBottomIfNeeded_ref_udaxihhe();

    // Create ResizeObserver to detect height changes
    const resizeObserver = new ResizeObserver(() => {
        scrollToBottomIfNeeded_ref_udaxihhe();
    });

    // Track scroll position before height changes
    container.addEventListener('scroll', checkIfNearBottom_ref_udaxihhe);

    // Initial check
    checkIfNearBottom_ref_udaxihhe();

    // Observe container for size changes
    resizeObserver.observe(container);

    return () => {
        container.removeEventListener('scroll', checkIfNearBottom_ref_udaxihhe);
        resizeObserver.disconnect();
    };
});



  return (
    jsx("div",{css:({ ["flex"] : "1", ["padding"] : "8px", ["overflow"] : "auto" }),id:"udaxihhe",ref:ref_udaxihhe},Array.prototype.map.call(reflex___state____state__reflex_chat___state____state.selected_chat_rx_state_ ?? [],((qa_rx_state_,index_0d2f45b46d5003d758f69f8d19431bcd)=>(jsx(RadixThemesBox,{css:({ ["maxWidth"] : "50em", ["marginInline"] : "auto" }),key:index_0d2f45b46d5003d758f69f8d19431bcd},jsx(RadixThemesBox,{css:({ ["textAlign"] : "right", ["marginBottom"] : "8px" })},jsx("div",{css:({ ["backgroundColor"] : "var(--mauve-4)", ["color"] : "var(--mauve-12)", ["display"] : "inline-block", ["paddingInline"] : "1em", ["borderRadius"] : "8px" })},jsx(ReactMarkdown,{components:ComponentMap_d59534cfa3df3086665270d8af3d1699(),rehypePlugins:[rehypeKatex, rehypeRaw, rehypeUnwrapImages],remarkPlugins:[remarkMath, remarkGfm]},qa_rx_state_?.["question"]))),jsx(RadixThemesBox,{css:({ ["textAlign"] : "left", ["marginBottom"] : "8px" })},jsx("div",{css:({ ["backgroundColor"] : "var(--accent-4)", ["color"] : "var(--accent-12)", ["display"] : "inline-block", ["paddingInline"] : "1em", ["borderRadius"] : "8px" })},jsx(ReactMarkdown,{components:ComponentMap_d59534cfa3df3086665270d8af3d1699(),rehypePlugins:[rehypeKatex, rehypeRaw, rehypeUnwrapImages],remarkPlugins:[remarkMath, remarkGfm]},qa_rx_state_?.["answer"]))))))))
  )
}


function Button_4fe2107efa7bfb00f45e2cdaf0e3977f () {
  const reflex___state____state__reflex_chat___state____state = useContext(StateContexts.reflex___state____state__reflex_chat___state____state)



  return (
    jsx(RadixThemesButton,{disabled:reflex___state____state__reflex_chat___state____state.processing_rx_state_,loading:reflex___state____state__reflex_chat___state____state.processing_rx_state_,type:"submit"},"Send")
  )
}


function Root_d3c959f5b71b16a63a888d20c39308b6 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);
const ref_question = useRef(null); refs["ref_question"] = ref_question;

    const handleSubmit_6a1a1ea40cc23f667b856cc4291fd392 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["question"] : getRefValue(refs["ref_question"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.reflex_chat___state____state.process_question", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (true) {
            $form.reset()
        }
    })
    


  return (
    jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_6a1a1ea40cc23f667b856cc4291fd392},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["maxWidth"] : "50em", ["margin"] : "0 auto", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(RadixThemesTextField.Root,{css:({ ["flex"] : "1" }),id:"question",placeholder:"Type something...",ref:ref_question},jsx(RadixThemesTextField.Slot,{},jsx(RadixThemesTooltip,{content:"Enter a question to get a response."},jsx(LucideInfo,{size:18},)))),jsx(Button_4fe2107efa7bfb00f45e2cdaf0e3977f,{},)))
  )
}


function Link_17367ce1eaa408918b5245d236b82862 () {
  const { resolvedColorMode } = useContext(ColorModeContext)



  return (
    jsx(RadixThemesLink,{asChild:true,css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) }),size:"3"},jsx(ReactRouterLink,{to:"https://reflex.dev"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["textAlign"] : "center", ["padding"] : "1em" }),direction:"row",gap:"3"},"Built with ",jsx("svg",{"aria-label":"Reflex",css:({ ["fill"] : ((resolvedColorMode?.valueOf?.() === "light"?.valueOf?.()) ? "#110F1F" : "white") }),height:"12",role:"img",width:"56",xmlns:"http://www.w3.org/2000/svg"},jsx("path",{d:"M0 11.5999V0.399902H8.96V4.8799H6.72V2.6399H2.24V4.8799H6.72V7.1199H2.24V11.5999H0ZM6.72 11.5999V7.1199H8.96V11.5999H6.72Z"},),jsx("path",{d:"M11.2 11.5999V0.399902H17.92V2.6399H13.44V4.8799H17.92V7.1199H13.44V9.3599H17.92V11.5999H11.2Z"},),jsx("path",{d:"M20.16 11.5999V0.399902H26.88V2.6399H22.4V4.8799H26.88V7.1199H22.4V11.5999H20.16Z"},),jsx("path",{d:"M29.12 11.5999V0.399902H31.36V9.3599H35.84V11.5999H29.12Z"},),jsx("path",{d:"M38.08 11.5999V0.399902H44.8V2.6399H40.32V4.8799H44.8V7.1199H40.32V9.3599H44.8V11.5999H38.08Z"},),jsx("path",{d:"M47.04 4.8799V0.399902H49.28V4.8799H47.04ZM53.76 4.8799V0.399902H56V4.8799H53.76ZM49.28 7.1199V4.8799H53.76V7.1199H49.28ZM47.04 11.5999V7.1199H49.28V11.5999H47.04ZM53.76 11.5999V7.1199H56V11.5999H53.76Z"},),jsx("title",{},"Reflex")))))
  )
}


export default function Component() {





  return (
    jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["backgroundColor"] : "var(--mauve-1)", ["color"] : "var(--mauve-12)", ["height"] : "100dvh", ["alignItems"] : "stretch" }),direction:"column",gap:"0"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["justifyContent"] : "space-between", ["alignItems"] : "center", ["padding"] : "12px", ["borderBottom"] : "1px solid var(--mauve-3)", ["backgroundColor"] : "var(--mauve-2)" }),direction:"row",gap:"3"},jsx(Badge_bc1564de00bf56a18cc809ef237fedde,{},),jsx(Dialog__root_55dde44f0a7bdd3058a1a49d59ddeaea,{},),jsx(VaulDrawer.Root,{direction:"left"},jsx(VaulDrawer.Trigger,{asChild:true},jsx(RadixThemesIconButton,{css:({ ["padding"] : "6px", ["backgroundColor"] : "var(--mauve-6)" })},jsx(LucideMessagesSquare,{},))),jsx(VaulDrawer.Overlay,{css:({ ["position"] : "fixed", ["left"] : "0", ["right"] : "0", ["bottom"] : "0", ["top"] : "0", ["zIndex"] : 50, ["background"] : "rgba(0, 0, 0, 0.5)" })},),jsx(VaulDrawer.Portal,{},jsx(RadixThemesTheme,{css:{...theme.styles.global[':root'], ...theme.styles.global.body}},jsx(VaulDrawer.Content,{css:({ ["left"] : "0", ["right"] : "auto", ["bottom"] : "0", ["top"] : "auto", ["position"] : "fixed", ["zIndex"] : 50, ["display"] : "flex", ["height"] : "100%", ["width"] : "20em", ["padding"] : "2em", ["backgroundColor"] : "var(--mauve-2)", ["outline"] : "none" })},jsx(Flex_20122bb049761b84fa7579d50fa6e001,{},)))))),jsx(Div_ae607de5d3e93df2d7764828faf96623,{},),jsx(RadixThemesFlex,{align:"stretch",css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["position"] : "sticky", ["bottom"] : "0", ["left"] : "0", ["paddingTop"] : "16px", ["paddingBottom"] : "16px", ["backdropFilter"] : "auto", ["backdropBlur"] : "lg", ["borderTop"] : "1px solid var(--mauve-3)", ["backgroundColor"] : "var(--mauve-2)", ["width"] : "100%" })},jsx(RadixThemesFlex,{align:"stretch",className:"rx-Stack",css:({ ["width"] : "100%", ["paddingInlineStart"] : "16px", ["paddingInlineEnd"] : "16px" }),direction:"column",gap:"3"},jsx(Root_d3c959f5b71b16a63a888d20c39308b6,{},),jsx(RadixThemesText,{as:"p",css:({ ["textAlign"] : "center", ["fontSize"] : ".75em", ["color"] : "var(--mauve-10)" })},"ReflexGPT may return factually incorrect or misleading responses. Use discretion."),jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["marginBlock"] : "-1em" })},jsx(Link_17367ce1eaa408918b5245d236b82862,{},))))),jsx("title",{},"ReflexChat | Index"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}